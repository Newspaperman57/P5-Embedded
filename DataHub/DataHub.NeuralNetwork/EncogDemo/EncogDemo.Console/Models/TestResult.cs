using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace DataHub.Messages
{
    public class TestResult
    {
        public int Id { get; set; }
        public DataSetResult[] DataSetResults { get; set; }
    }
}