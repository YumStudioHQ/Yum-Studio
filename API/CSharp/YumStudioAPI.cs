using Godot;

namespace YumStudio.API;

/// <summary>
/// Public static class that provides global members that can be used in programs.
/// </summary>
public static class YumStudioInstance
{
  /// <summary>
  /// Fired once, when the Runtime starts up the game.
  /// </summary>
  public static readonly HotSpot<string[]> InitSpot;

  /// <summary>
  /// Called each frames, giving the delta as argument.
  /// </summary>
  public static readonly HotSpot<double> ProcessSpot;

  /// <summary>
  /// Called each frames, giving the delta as argument.
  /// </summary>
  public static readonly HotSpot<double> PhysicProcessSpot;

  /// <summary>
  /// Called when any input is pressed
  /// </summary>
  public static readonly HotSpot<InputEvent> EventSpot;

  /// <summary>
  /// Called before exiting Runtime's process (at the end of the game).
  /// </summary>
  public static readonly HotSpot ExitSpot;

  /// <summary>
  /// Returns the root node.
  /// </summary>
  /// <returns>Root node</returns>
  public static Node GetRoot() => YumStudioKernelInterface.GetRootNote();
}

internal static class YumStudioKernelInterface
{
  private static Node kernelRoot;

  public static void YumStudioEntry(Node root)
  {
    kernelRoot = root;
  }

  public static void YumStudioFireInit(string[] args) => YumStudioInstance.InitSpot.Fire(args);
  public static void YumStudioFireProcess(double delta) => YumStudioInstance.ProcessSpot.Fire(delta);
  public static void YumStudioFirePhysicProcess(double delta) => YumStudioInstance.ProcessSpot.Fire(delta);
  public static void YumStudioFireEvent(InputEvent @event) => YumStudioInstance.EventSpot.Fire(@event);
  public static void YumStudioFireExit() => YumStudioInstance.ExitSpot.Fire();
  public static Node GetRootNote() => kernelRoot;

}