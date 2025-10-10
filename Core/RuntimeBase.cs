using Godot;

namespace YumStudio.Core;

public partial class RuntimeBase : Node
{
  public void Init()
  {
    API.YumStudioKernelInterface.YumStudioEntry(this);
    API.YumStudioKernelInterface.YumStudioFireInit(OS.GetCmdlineArgs());
  } 

  public override void _Process(double delta)
   => API.YumStudioKernelInterface.YumStudioFireProcess(delta);

  public override void _Input(InputEvent @event)
    => API.YumStudioKernelInterface.YumStudioFireEvent(@event); 
}