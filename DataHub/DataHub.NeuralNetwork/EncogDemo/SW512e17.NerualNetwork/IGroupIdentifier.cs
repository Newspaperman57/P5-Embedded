using System;
using System.Collections.Generic;
using System.Text;

namespace SW512e17.NerualNetwork
{
    public interface IGroupIdentifier
    {
        Group[] Identify(DataPoint[] data);
    }
}
