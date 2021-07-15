using System;
namespace assembly
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello world\r\nArgs:");

            foreach(string arg in args)
            {
                Console.Write("{0}\r\n", arg);
            }
        }
    }
}
