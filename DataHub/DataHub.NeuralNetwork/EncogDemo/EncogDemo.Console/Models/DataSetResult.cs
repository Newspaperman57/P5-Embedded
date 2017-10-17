using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace DataHub.Messages
{
    public class DataSetResult
    {
        public int DataSetId { get; set; }
        public Classification[] Classifications { get; set; }
    }
}