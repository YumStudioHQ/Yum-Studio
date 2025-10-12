using System;
using System.Diagnostics;

namespace YumStudio.Core.UnderlyingSystem;

public static class Applications
{
  public static string GetApplicationPath(string name)
  {
    string cmd;
    string args;

    if (OperatingSystem.IsWindows())
    {
      cmd = "where";
      args = name;
    }
    else
    {
      cmd = "which";
      args = name;
    }

    var process = new Process
    {
      StartInfo = new ProcessStartInfo
      {
        FileName = cmd,
        Arguments = args,
        RedirectStandardOutput = true,
        UseShellExecute = false,
        CreateNoWindow = true
      }
    };

    process.Start();
    string result = process.StandardOutput.ReadToEnd().Trim();
    process.WaitForExit();

    return string.IsNullOrWhiteSpace(result) ? "" : result.Split('\n')[0].Trim();
  }
}
