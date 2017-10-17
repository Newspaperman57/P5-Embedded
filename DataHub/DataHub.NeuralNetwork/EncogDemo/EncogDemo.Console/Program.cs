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
using SW512e17.NerualNetwork;
using System.Collections.Generic;
using Encog.Util.KMeans;
using System.IO;
using System.Net.Http;
using DataHub.Messages;

namespace EncogDemo.Demo
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            //// create a neural network, without using a factory
            //int inputFrame = 40;
            //var network = new BasicNetwork();
            //network.AddLayer(new BasicLayer(null, true, inputFrame));
            //network.AddLayer(new BasicLayer(new ActivationSigmoid(), true, 40));
            //network.AddLayer(new BasicLayer(new ActivationSigmoid(), true, 20));
            //network.AddLayer(new BasicLayer(new ActivationSigmoid(), false, 2));
            //network.Structure.FinalizeStructure();
            //network.Reset();

            //Mapping[] mappings = new Mapping[]
            //{
            //    new Mapping { Path = "mortenvsgrunberg.csv", Output = new double[] { 1, 0 } },
            //    //new Mapping { Path = "grunbergcsmorten.csv", Output = new double[] { 0, 1 } },
            //    //new Mapping { Path = "mortenvsgrunberg_rematch.csv", Output = new double[] { 1, 0 } },
            //    new Mapping { Path = "grunbergvsmorten_rematch.csv", Output = new double[] { 0, 1 } },
            //};
            //Random rnd = new Random();

            //var dataSet = DataSetFactory.FromCsvFiles(mappings, d => new double[] { d.X / 2000, d.Y / 2000, d.Z / 2000, d.RX / 10000 } /*new double[] { rnd.NextDouble(), rnd.NextDouble(), rnd.NextDouble(), rnd.NextDouble() }*/, inputFrame);

            //List<double> randomSequence = new List<double>();

            //for (int i = 0; i < 10000; i++)
            //{
            //    randomSequence.Add(rnd.NextDouble());
            //}

            //int c = 0;
            //dataSet.InputSet = dataSet.InputSet.OrderBy(d => randomSequence[c++ % 10000]).ToArray();
            //c = 0;
            //dataSet.OutputSet = dataSet.OutputSet.OrderBy(d => randomSequence[c++ % 10000]).ToArray();

            //int trainSize = 200;

            //// create training data
            //IMLDataSet trainingSet = new BasicMLDataSet(dataSet.InputSet.Take(trainSize).ToArray(), dataSet.OutputSet.Take(trainSize).ToArray());
            //IMLDataSet testSet = new BasicMLDataSet(dataSet.InputSet.Skip(trainSize).ToArray(), dataSet.OutputSet.Skip(trainSize).ToArray());

            //// train the neural network
            //IMLTrain train = new ResilientPropagation(network, trainingSet);

            //int epoch = 1;

            //do
            //{
            //    train.Iteration();
            //    if (epoch % 1000 == 0)
            //        Console.WriteLine(@"Epoch #" + epoch + @" Error:" + train.Error);
            //    epoch++;
            //} while (train.Error > 0.01);

            //train.FinishTraining();

            //// test the neural network
            ////Console.WriteLine(@"Neural Network Results:");
            //int correct = 0, wrong = 0;
            //foreach (IMLDataPair pair in testSet)
            //{
            //    IMLData output = network.Compute(pair.Input);
            //    if (output[0] > output[1] && pair.Ideal[0] == 1) //Morten
            //        correct++;
            //    else if (output[0] < output[1] && pair.Ideal[1] == 1)
            //        correct++;
            //    else
            //        wrong++;
            //    //Console.WriteLine("actual=" + string.Join(" ", output) + @" ,ideal=" + string.Join(" ", pair.Ideal));
            //}



            //Console.WriteLine($"{correct} / {correct + wrong} = {(double)correct / ((double)correct + wrong) * 100 + " %"}");

            //            "mortenvsgrunberg.csv", Output = new double[] { 1, 0 } },
            //                new Mapping { Path = "grunbergcsmorten.csv", Output = new double[] { 0, 1 }
            //                new Mapping { Path = "mortenvsgrunberg_rematch.csv", Output = new double[] { 1, 0 } },
            //                new Mapping { Path = "grunbergvsmorten_rematch.csv"

            string[] files = new string[]
            {
                "0210/mortenvsanton.csv",
                "0210/mortenvsgrunberg.csv",
                "0210/grunbergvsanton.csv",
                "0210/grunbergvsmorten.csv",
                "mortenvsgrunberg_rematch.csv",
                "grunbergcsmorten.csv",
                "9-21 Morten 5mål.csv",
                "1506329500_mortensKick2.csv",
                "1506330115_grundbergtest.csv",
            };
            //int inputFrame = 40;
            //FileInfo networkFile = new FileInfo(@"model/network.eg");
            //var network = (BasicNetwork)(Encog.Persist.EncogDirectoryPersistence.LoadObject(networkFile));

            //foreach (var f in files)
            //{

            //    var da = new DataParser().ParseCsv(f);
            //    var gr = new ShotIdentifier().Identify(da);

            //    int morten = 0, grunberg = 0;

            //    //Console.WriteLine($"Morten skud: {dataSet.OutputSet.Where(d => d[0] == 1).Count()}    Grunberg skud: {dataSet.OutputSet.Where(d => d[1] == 1).Count()}");

            //    foreach (var g in gr)
            //    {
            //        List<double> input = new List<double>();
            //        if (g.Data.Length > inputFrame)
            //        {
            //            foreach (var item in g.Data.Take(40).Select(d => new double[] { d.X / 2000, d.Y / 2000, d.Z / 2000, d.RX / 10000 }))
            //            {
            //                foreach (var item2 in item)
            //                {
            //                    input.Add(item2);
            //                }
            //            }
            //            IMLData output = network.Compute(new BasicMLData(input.ToArray()));
            //            if (output[0] > output[1]) //Morten
            //                morten++;
            //            else
            //                grunberg++;
            //        }
            //    }
            //    //Console.WriteLine($"Morten: {morten}   Grunberg: {grunberg}");
            //    Console.WriteLine(f + ": " + (morten > grunberg ? "Morten" : "Grunberg"));
            //}
            ////Encog.Persist.EncogDirectoryPersistence.SaveObject(networkFile, (BasicNetwork)network);

            HttpClient client = new HttpClient();

            client.BaseAddress = new Uri("http://p5datahub.azurewebsites.net");

            var tests = client.GetAsync("/api/modeltype/21/test");

            Console.WriteLine("Sending request");

            var testInfo = Newtonsoft.Json.JsonConvert.DeserializeObject<Response<TestInfo>>(tests.Result.Content.ReadAsStringAsync().Result).Data;

            Console.WriteLine("Received request");

            Dictionary<int, List<Group>> trainData = new Dictionary<int, List<Group>>();

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
                        if(trainData.ContainsKey(label.Id) && group.Data.Length > 10)
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

            List<double[]> inputs = new List<double[]>();
            List<double[]> outputs = new List<double[]>();

            int i = 0;

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

            IMLDataSet dataset = new BasicMLDataSet(inputs.ToArray(), outputs.ToArray());


            Console.WriteLine("Converted");

            var network = new BasicNetwork();
            network.AddLayer(new BasicLayer(null, true, 40));
            network.AddLayer(new BasicLayer(new ActivationSigmoid(), true, int.Parse(testInfo.Parameters.First(pa => pa.Name == "HiddenNeurons").Value)));
            network.AddLayer(new BasicLayer(new ActivationSigmoid(), false, testInfo.Labels.Length));
            network.Structure.FinalizeStructure();
            network.Reset();

            IMLTrain train = new ResilientPropagation(network, dataset);

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

            TestResult result = new TestResult()
            {
                DataSetResults = datasetResults.ToArray()
            };

            var content = new StringContent(Newtonsoft.Json.JsonConvert.SerializeObject(result));

            content.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");

            var post = client.PostAsync("api/test/" + testInfo.Id + "/result", content);


            var res = post.Result.Content.ReadAsStringAsync();

            Console.WriteLine(res.Result);

            Console.ReadLine();

            EncogFramework.Instance.Shutdown();
        }
    }
}
