using System;
using System.Collections.Generic;
using System.IO;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.Engine.Cycles;

namespace YumStudio.Core.Engine.Editor.Projects;

[OnEngineReady]
public static class ProjectSection
{
  public static readonly Dictionary<string, ProjectFile> Projects = [];

  public static void Init()
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
          var projname = proj.Key.Trim();
          var projpath = proj.Value;

          if (!File.Exists(projpath))
          {
            Output.Error($"'{projpath}': No such path!");
            continue;
          }

          try
          {
            // TODO ? Handle projects with the same name
            Projects[projname] = ProjectFile.FromFile(projpath);
          }
          catch (Exception e)
          {
            Output.Error($"Error: {e}");
            continue;
          }
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
      Output.Error($"C# Exception at {typeof(ProjectSection).FullName}", e.ToString());
    }
  }
}