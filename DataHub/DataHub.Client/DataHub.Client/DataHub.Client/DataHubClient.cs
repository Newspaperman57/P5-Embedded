using System;
using Encog.Neural.Networks;
using Encog.Neural.Networks.Layers;
using Encog.Engine.Network.Activation;
using Encog.ML.Data;
using Encog.Neural.Networks.Training.Propagation.Resilient;
using Encog.ML.Train;
using Encog.ML.Data.Basic;
using Encog;
using System.Linq;
using System.Collections.Generic;
using Encog.Util.KMeans;
using System.IO;
using System.Net.Http;
using DataHub.Messages;
using DataHub.Grouping;

namespace DataHub.Client
{
    class DataHubClient
    {
        public string ModelTypeID { get; set; }
        public Dictionary<int, List<Group>> trainData = new Dictionary<int, List<Group>>();
        HttpClient client = new HttpClient();

        public DataHubClient(string modelTypeID)
        {
            ModelTypeID = modelTypeID;

        }

        public TestInfo GetTestInfo()
        {
            client.BaseAddress = new Uri("http://p5datahub.azurewebsites.net");

            var tests = client.GetAsync("/api/modeltype/"+ModelTypeID+"/test");

            Console.WriteLine("Sending request");

            var tI = Newtonsoft.Json.JsonConvert.DeserializeObject<Response<TestInfo>>(tests.Result.Content.ReadAsStringAsync().Result).Data;

            Console.WriteLine("Received request");

            return tI;
        }

        public void IdentifyData()
        {
            TestInfo testInfo = GetTestInfo();

            foreach (var label in testInfo.Labels)
            {
                trainData.Add(label.Id, new List<Group>());
            }

            var shotIdentifier = new ShotIdentifier();

            Console.WriteLine("Identifying");

            foreach (var trainSet in testInfo.TrainingSet)
            {
                var data = trainSet.Data.Select(d => new DataPoint()
                {
                    Time = d.Time,
                    RX = d.RX,
                    RY = d.RY,
                    RZ = d.RZ,
                    X = d.X,
                    Y = d.Y,
                    Z = d.Z
                }).ToArray();
                var groups = shotIdentifier.Identify(data);
                foreach (var group in groups)
                {
                    foreach (var label in trainSet.Labels)
                    {
                        if (trainData.ContainsKey(label.Id) && group.Data.Length > 10)
                            trainData[label.Id].Add(group);
                    }
                }
            }

            Console.WriteLine("Identified");

            int min = trainData.Min(d => d.Value.Count);

            Console.WriteLine(min);

            foreach (var key in trainData.Keys.ToArray())
            {
                trainData[key] = trainData[key].Take(min).ToList();
            }
        }

        public BasicMLDataSet ConvertData()
        {
            List<double[]> inputs = new List<double[]>();
            List<double[]> outputs = new List<double[]>();

            int i = 0;
            TestInfo testInfo = GetTestInfo();


            Console.WriteLine("Converting");


            foreach (var key in trainData.Keys)
            {
                foreach (var group in trainData[key])
                {
                    List<double> input = new List<double>();

                    foreach (var data in group.Data.Take(10))
                    {
                        input.Add(data.X / 2000);
                        input.Add(data.Y / 2000);
                        input.Add(data.Z / 2000);
                        input.Add(data.RX / 10000);
                    }

                    double[] output = new double[trainData.Keys.Count];
                    output[i] = 1;
                    inputs.Add(input.ToArray());
                    outputs.Add(output);
                }

                i++;
            }




            List<double> randomSequence = new List<double>();

            Random rnd = new Random();

            for (int w = 0; w < 10000; w++)
            {
                randomSequence.Add(rnd.NextDouble());
            }

            int p = 0;
            inputs = inputs.OrderBy(d => randomSequence[p++ % 10000]).ToList();
            p = 0;
            outputs = outputs.OrderBy(d => randomSequence[p++ % 10000]).ToList();

            Console.WriteLine("Converted");

            return new BasicMLDataSet(inputs.ToArray(), outputs.ToArray());
        }

        // This is where I should make it generic, so that it works for multiple methods, and not just NN specifically, with only 3 parameters
        public TestResult Train()
        {
            BasicMLDataSet dataset = ConvertData();
            TestInfo testInfo = GetTestInfo();


            var network = new BasicNetwork();
            network.AddLayer(new BasicLayer(null, true, 40));
            network.AddLayer(new BasicLayer(new ActivationSigmoid(), true, int.Parse(testInfo.Parameters.First(pa => pa.Name == "HiddenNeurons").Value)));
            network.AddLayer(new BasicLayer(new ActivationSigmoid(), false, testInfo.Labels.Length));
            network.Structure.FinalizeStructure();
            network.Reset();

            IMLTrain train = new ResilientPropagation(network, dataset);

            TestInfo testInfo = GetTestInfo();
            ShotIdentifier shotIdentifier = new ShotIdentifier();

            int epoch = 1;
            Console.WriteLine("Training");

            double old = 0, newErr = 0;

            do
            {
                train.Iteration();
                old = newErr;
                newErr = train.Error;
                Console.WriteLine(@"Epoch #" + epoch + @" Error:" + train.Error + " Diff:" + Math.Abs(old - newErr));

                epoch++;
            } while ((train.Error > 0.00000000000000001 && Math.Abs(old - newErr) > 0.000000001 || epoch < int.Parse(testInfo.Parameters.First(pa => pa.Name == "MinIterations").Value)) && epoch < int.Parse(testInfo.Parameters.First(pa => pa.Name == "MaxIterations").Value));

            train.FinishTraining();

            Console.WriteLine(string.Join(" ", trainData.Keys.Select(k => testInfo.Labels.First(l => l.Id == k).Name + "(" + trainData.Where(t => t.Key == k).Sum(q => q.Value.Count) + ")")));

            List<DataSetResult> datasetResults = new List<DataSetResult>();

            foreach (var testSet in testInfo.TestSet)
            {
                double[] confidence = new double[testInfo.Labels.Length];
                int no = 0;
                var data = testSet.Data.Select(d => new DataPoint()
                {
                    Time = d.Time,
                    RX = d.RX,
                    RY = d.RY,
                    RZ = d.RZ,
                    X = d.X,
                    Y = d.Y,
                    Z = d.Z
                }).ToArray();
                var groups = shotIdentifier.Identify(data);
                foreach (var group in groups)
                {

                    if (group.Data.Length > 10)
                    {
                        List<double> input = new List<double>();
                        foreach (var d in group.Data.Take(10))
                        {
                            input.Add(d.X / 2000);
                            input.Add(d.Y / 2000);
                            input.Add(d.Z / 2000);
                            input.Add(d.RX / 10000);
                        }
                        var output = network.Compute(new BasicMLData(input.ToArray()));
                        for (int n = 0; n < output.Count; n++)
                        {
                            confidence[n] += output[n];
                        }
                        no++;
                    }
                }

                confidence = confidence.Select(c => c / no).ToArray();

                List<Classification> classifications = new List<Classification>();

                for (int e = 0; e < testInfo.Labels.Length; e++)
                {
                    classifications.Add(new Classification()
                    {
                        Confidence = confidence[e],
                        LabelId = testInfo.Labels[e].Id
                    });
                }

                datasetResults.Add(new DataSetResult()
                {
                    DataSetId = testSet.Id,
                    Classifications = classifications.ToArray()
                });

                Console.WriteLine(testSet.Name + ": " + string.Join(" ", confidence.Select(c => Math.Round(c * 100) / 100)));
            }

            return new TestResult()
            {
                ModelId = testInfo.ModelId,
                DataSetResults = datasetResults.ToArray()
            };
        }

        public Response<TestResult> SendTestResult()
        {
            TestResult testResult = Train();
            var testInfo = GetTestInfo();
            var content = new StringContent(Newtonsoft.Json.JsonConvert.SerializeObject(result));
            var post = client.PostAsync("api/test/" + testInfo.Id + "/result", content);

            content.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");

            return Newtonsoft.Json.JsonConvert.DeserializeObject<Response<TestResult>>(post.Result.Content.ReadAsStringAsync().Result);
        }

    }
}
