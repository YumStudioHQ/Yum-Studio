using System;
using System.Collections.Generic;
using System.IO;
using YumStudio.Core.Engine.Editor.Modules.Resources;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.UnderlyingSystem;

namespace YumStudio.Core.Engine.Editor.Projects;

public static class ProjectManager
{
  private static readonly List<string> ApiFileDirectories = [
    ResourcesManager.RELATIVE_INTERNAL,
    ResourcesManager.RELATIVE_IMPORT,
    ResourcesManager.RELATIVE_NODES,
    ResourcesManager.RELATIVE_GEN,
    ResourcesManager.RELATIVE_GENNODE,
  ];

  private static void CopyApi(string path)
  {
    foreach (var item in ApiFileDirectories)
    {
      FileSystem.CopyDirectory(item, path, true);
    }
  }

  private static void CreateProjectFile(string name, string path)
  {
    YSObject obj = YSObject.CreateTemplate<ProjectFile>("project", true); // standardize = true will convert names snackcase.
    obj["project"]["name"] = name;
    obj["project"]["path"] = path;
    var proj_path = Path.Join(path, ".ysproj.yso");
    obj.Save(proj_path,
    "; YumStudio configuration file\n; Prefer using YumStudio.Editor to edit that file.");
    ProjectSection.Projects[name] = new(name, path);
  }

  private static void CreateCSharpProject(string name, string path)
  {
    int code = Execution.Execute("dotnet", ["new", "classlib", "-n", name, "-o", path, "--force"]);
    if (!DotnetJoke.IsSuccess(code))
      throw new InvalidProgramException(DotnetJoke.Describe(code));

    var csprojPath = Path.Combine(path, $"{name}.csproj");

    // replace SDK type
    var lines = File.ReadAllLines(csprojPath);
    if (lines.Length > 0 && lines[0].StartsWith("<Project Sdk=\"Microsoft.NET.Sdk"))
    {
      lines[0] = "<Project Sdk=\"Godot.NET.Sdk/4.0.0\">";
      File.WriteAllLines(csprojPath, lines);
    }

    Output.Log($"C#: {DotnetJoke.Describe(code)} (Godot SDK patched)");
  }


  public static TaskPipeline CreateProject(string name, string path)
  {
    return new([
      new("Creating root directory", () => Directory.CreateDirectory(path)),
      new("Copying YumStudio API", () => CopyApi(path)),
      new("Creating project file", () => CreateProjectFile(name, path)),
      new("Creating C# project", () => CreateCSharpProject(name, path)),
      new("Done", () => Output.Success($"Project created {Output.Color.BrightMagenta}{name}{Output.Color.Reset} at {path}"))
    ]);
  }
}