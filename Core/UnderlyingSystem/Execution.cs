using System;
using System.Diagnostics;
using System.Linq;

namespace YumStudio.Core.UnderlyingSystem;

public static class Execution
{
  public static string ArgumentArrayAsString(string[] args)
  {
    string s = "";
    foreach (var arg in args) s += $" \"{arg}\" ";
    return s;
  }

  public static int Execute(string appname, string[] args)
  {
    var process = new Process()
    {
      StartInfo = new ProcessStartInfo()
      {
        FileName = Applications.GetApplicationPath(appname),
        Arguments = ArgumentArrayAsString(args),
        CreateNoWindow = true,
        UseShellExecute = false,
      }
    };

    process.Start();
    process.WaitForExit();

    return process.ExitCode;  
  }
}