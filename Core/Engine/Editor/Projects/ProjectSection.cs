using System;
using System.Collections.Generic;
using System.IO;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.Engine.Cycles;
using YumStudio.Utility;
using Godot;

namespace YumStudio.Core.Engine.Editor.Projects;

[OnEngineReady][OnYumStudioShutdown] // YumStudio's Shutdown is the first. So we ensure we write everything before GlobalInstance.
public class ProjectSection
{
  public const string PROJECT_SECTION = "projects";

  public static readonly Dictionary<string, ProjectFile> Projects = [];

  public static void InitEngine()
  {
    try
    {
      var projects = YSObject.Parse(Globals.ConfigFile, true);
      Output.Info($"Loading internal file {Output.Color.Green}{Globals.ConfigFile}{Output.Color.Reset}");

      if (!projects.HasScope(PROJECT_SECTION))
      {
        // Create scope and then return -- cannot initialize nothing..
        projects[PROJECT_SECTION] = [];
      }
      else
      {
        var list = projects[PROJECT_SECTION];
        foreach (var proj in list)
        {
          var projname = proj.Key.Trim();
          var projpath = proj.Value.Trim();

          if (!File.Exists(projpath))
          {
            Output.Error($"'{projpath}': No such path!");
            continue;
          }

          try
          {
            Projects[projname] = ProjectFile.FromFile(projpath);
            Output.Info($"{Output.Color.Reset}Found project {Output.Color.BrightMagenta}{projname}{Output.Color.Reset} {projpath}");
          }
          catch (Exception e)
          {
            Output.Error($"Error: {e}");
            continue;
          }
        }
      }

      projects.Save(Globals.ConfigFile, Globals.ConfigFileHeader);
      Output.Log(projects.ToString());
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

  public static void ShutdownYumStudio()
  {
    var glob = YSObject.Parse(Globals.ConfigFile, true);
    if (!glob.HasScope(PROJECT_SECTION)) glob[PROJECT_SECTION] = [];
    foreach (var project in Projects)
    {
      glob[PROJECT_SECTION][project.Value.Name] = Path.Combine(project.Value.Path, ".ysproj.yso");
      Output.Log(glob.ToString());
    }
    glob.Save(Globals.ConfigFile, Globals.ConfigFileHeader);
  }
}