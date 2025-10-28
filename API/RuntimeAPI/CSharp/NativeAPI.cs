using System;
using System.Runtime.InteropServices;

namespace YumStudio.Native
{
  // Constants
  public static class NativeConstants
  {
    public const ulong INVALID_NODE = ulong.MaxValue;
  }

  // Delegate definitions (function pointers)
  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate ulong ysnative_create();

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysnative_queuefree(ulong node);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysnative_get_children(ulong node, [Out] ulong[] buffer, ulong count);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate ulong ysnative_get_parent(ulong node);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysnative_get_parents(ulong node, [Out] ulong[] buffer, ulong count);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate ulong ysnative_get_node([MarshalAs(UnmanagedType.LPStr)] string nodeName);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysnative_add_child(ulong parent, ulong child);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysnative_add_children(ulong parent, [In] ulong[] nodes, ulong count);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysgd_callback(IntPtr[] argv, ulong argc);

  [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
  public delegate void ysnative_connect(ulong node, [MarshalAs(UnmanagedType.LPStr)] string methodName, ysgd_callback callback);

  [StructLayout(LayoutKind.Sequential)]
  public struct YSNative
  {
    public IntPtr add_child;
    public IntPtr add_children;
    public IntPtr connect;
    public IntPtr get_node;
    public IntPtr get_parent;
    public IntPtr get_parents;
    public IntPtr create;
    public IntPtr queuefree;

    public readonly ysnative_add_child AddChild => Marshal.GetDelegateForFunctionPointer<ysnative_add_child>(add_child);
    public readonly ysnative_add_children AddChildren => Marshal.GetDelegateForFunctionPointer<ysnative_add_children>(add_children);
    public readonly ysnative_connect Connect => Marshal.GetDelegateForFunctionPointer<ysnative_connect>(connect);
    public readonly ysnative_get_node GetNode => Marshal.GetDelegateForFunctionPointer<ysnative_get_node>(get_node);
    public readonly ysnative_get_parent GetParent => Marshal.GetDelegateForFunctionPointer<ysnative_get_parent>(get_parent);
    public readonly ysnative_get_parents GetParents => Marshal.GetDelegateForFunctionPointer<ysnative_get_parents>(get_parents);
    public readonly ysnative_create Create => Marshal.GetDelegateForFunctionPointer<ysnative_create>(create);
    public readonly ysnative_queuefree QueueFree => Marshal.GetDelegateForFunctionPointer<ysnative_queuefree>(queuefree);
  }

  internal static class NativeAPI
  {
    [DllImport("YumStudioNative", CallingConvention = CallingConvention.Cdecl)]
    private static extern IntPtr ys_get_native();

    public static YSNative GetNative()
    {
      IntPtr ptr = ys_get_native();
      if (ptr == IntPtr.Zero)
        throw new InvalidOperationException("Failed to retrieve native interface pointer.");

      return Marshal.PtrToStructure<YSNative>(ptr);
    }
  }
}
