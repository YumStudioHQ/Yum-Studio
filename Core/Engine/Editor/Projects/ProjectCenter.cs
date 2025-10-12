using System;
using System.IO;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.Engine.Entry;

namespace YumStudio.Core.Engine.Editor.Projects;

[OnEngineReady]
public class ProjectCenter
{
  public ProjectCenter()
  {
    try
    {
      var projects = YSObject.Parse(Globals.ConfigFile, true);
      Output.Info($"Loading internal file {Output.Color.Green}{Globals.ConfigFile}");

      if (!projects.HasScope("projects"))
      {
        // Create scope and then return -- cannot initialize nothing..
        projects["projects"] = [];
      }
      else
      {
        var list = projects["projects"];
        foreach (var proj in list)
        {
          
        }
      }

      projects.Save(Globals.ConfigFile, Globals.ConfigFileHeader);
    }
    catch (FileNotFoundException)
    {
      Output.Info($"Creating file {Output.Color.Green}{Globals.ConfigFile}");
      new YSObject().Save(Globals.ConfigFile, Globals.ConfigFileHeader);
    }
    catch (Exception e)
    {
      Output.Error($"C# Exception at {GetType().FullName}", e.ToString());
    }
  }
}