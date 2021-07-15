using System.Reflection;

namespace wrapper
{
    class Program
    {
        static void Main()
        {
            string[] Parameters = {/*REPLACEME*/};
            Assembly Target = Assembly.Load(Properties.Resources.assembly);
            Target.EntryPoint.Invoke(null, new object[] { Parameters });
        }
    }
}
