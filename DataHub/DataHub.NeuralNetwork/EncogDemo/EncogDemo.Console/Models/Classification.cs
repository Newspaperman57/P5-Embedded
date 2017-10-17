using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace DataHub.Messages
{
    public class Classification
    {
        public int LabelId { get; set; }
        public double Confidence { get; set; }
    }
}