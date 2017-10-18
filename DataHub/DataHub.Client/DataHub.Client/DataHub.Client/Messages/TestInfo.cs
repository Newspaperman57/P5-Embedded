using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataHub.Client.Messages
{
    class TestInfo
    {
        public int Id { get; set; }
        public int ModelId { get; set; }
        public int ModelTypeId { get; set; }
        public Label[] Labels { get; set; }
        public Parameter[] Parameters { get; set; }
        public DataLabelSet[] TrainingSet { get; set; }
        public TestDataSet[] TestSet { get; set; }
    }
}
