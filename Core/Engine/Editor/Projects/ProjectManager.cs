using System.Collections.Generic;
using System.IO;

namespace YumStudio.Core.Engine.Editor.Projects;

public static class ProjectManager
{
  private static readonly List<string> ApiFileDirectories = [];

  private static void CopyApi(string path)
  {
    foreach (var item in ApiFileDirectories)
    {
      EngineIO.FileSystem.CopyDirectory(item, path, true);
    }
  }

  public static TaskPipeline CreateProject(string name, string path)
  {
    return new([
      new("Creating root directory", () => Directory.CreateDirectory(path)),
      new("Copying YumStudio API", () => CopyApi(path)),
    ]);
  }
}