using System;
using System.Collections.Generic;
using System.IO;
using Godot;
using YumStudio.Core.Engine.EngineIO;
using YumStudio.Core.UnderlyingSystem;

namespace YumStudio.Core.Engine.Editor.Projects;

public static class ProjectManager
{
  private static readonly List<string> ApiFileDirectories = [];

  private static void CopyApi(string path)
  {
    foreach (var item in ApiFileDirectories)
    {
      FileSystem.CopyDirectory(item, path, true);
    }
  }

  private static void CreateProjectFile(string name, string path)
  {
    YSObject obj = YSObject.CreateTemplate<ProjectFile>("project");
    obj["project"]["name"] = name; // TODO?
    obj["project"]["path"] = path; // TODO?
    obj.Save(Path.Join(path, ".ysproj.yso"),
    "; YumStudio configuration file\n; Prefer using YumStudio.Editor to edit that file.");
    // TODO register in YumStudioGlobIdkWhat
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
    ]);
  }
}