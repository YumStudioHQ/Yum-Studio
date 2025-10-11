using System.IO;

namespace YumStudio.Core.Engine.Editor.Projects;

public class ProjectFile
{
  public string Name { get; private set; }
  public string Path { get; private set; }

  public ProjectFile() {}
  public ProjectFile(string name, string path) { Name = name; Path = path; }

  public static ProjectFile FromFile(string path)
  {
    if (!File.Exists(path)) throw new FileNotFoundException($"No such file '{path}'");
    
    return new();
  }
}