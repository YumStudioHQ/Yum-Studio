using YumStudio.Core.Engine.Entry;

namespace YumStudio.Core.Engine.Editor.Projects;

[OnEngineReady]
public class ProjectCenter
{
  public ProjectCenter()
  {
    var projects = YSObject.Parse(Globals.ConfigFile, true);

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
}