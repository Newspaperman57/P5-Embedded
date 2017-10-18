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
// below are two things, which may be needed to be included
//using SW512e17.NerualNetwork;
//using DataHub.Messages;

namespace DataHub.Client
{
    class Program
    {
        static void Main(string[] args)
        {
            // Initialise a base client for sending/receiving http requests
            HttpClient client = new HttpClient();

            client.BaseAddress = new Uri("http://p5datahub.azurewebsites.net");

            string id = "21";
            string specificModelID = "/api/modeltype/"+id+"/test";

            var tests = client.GetAsync(specificModelID);


        }
    }
}
