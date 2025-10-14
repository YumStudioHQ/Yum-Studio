using System.IO;

namespace YumStudio.Core.Engine.Editor.Projects;

public class ProjectFile
{
  public string Name { get; set; } = "";
  public string Path { get; set; } = "";
  public string Kind { get; set; } = "";

  public ProjectFile() { }
  public ProjectFile(string name, string path) { Name = name; Path = path; }

  public static ProjectFile FromFile(string path)
  {
    if (!File.Exists(path)) throw new FileNotFoundException($"No such file '{path}'");
    
    return YSObject.FromYSObject<ProjectFile>(YSObject.Parse(path, true), "ys.project");
  }
}