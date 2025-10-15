using System;
using Godot;

namespace YumStudio.Core.Engine.EngineIO;

/// <summary>
/// Static class that exposes basic functions to 
/// properly have Input/Output interactions with the Engine, including ANSI-colored output.
/// </summary>
public static class Output
{
  // ANSI color codes
  public static class Color
  {
    public const string Reset = "\u001b[0m";
    public const string Black = "\u001b[30m";
    public const string Red = "\u001b[31m";
    public const string Green = "\u001b[32m";
    public const string Yellow = "\u001b[33m";
    public const string Blue = "\u001b[34m";
    public const string Magenta = "\u001b[35m";
    public const string Cyan = "\u001b[36m";
    public const string White = "\u001b[37m";

    public const string BrightBlack = "\u001b[90m";
    public const string BrightRed = "\u001b[91m";
    public const string BrightGreen = "\u001b[92m";
    public const string BrightYellow = "\u001b[93m";
    public const string BrightBlue = "\u001b[94m";
    public const string BrightMagenta = "\u001b[95m";
    public const string BrightCyan = "\u001b[96m";
    public const string BrightWhite = "\u001b[97m";
  }

  public static void Write(string s)
  {
    Console.Write(s);
  }
  
  public static void WriteLine(string s)
  {
    Console.WriteLine(s);
  }

  /// <summary>
  /// Logs one or more messages to the console, optionally with a color.
  /// </summary>
  /// <param name="color">ANSI color code, default is reset.</param>
  /// <param name="args">Messages to log.</param>
  public static void Log(string color = Color.Reset, params string[] args)
  {
    if (args == null || args.Length == 0) return;

    Write($"{Color.Blue}[YumStudio]: {Color.Reset}{color}{args.Join("")}{Color.Reset}");
  }

  /// <summary>
  /// Shortcut for error messages in red.
  /// </summary>
  public static void Error(params string[] args)
  {
    Log(Color.Red, [..args, "\n"]);
  }

  /// <summary>
  /// Shortcut for info messages in cyan.
  /// </summary>
  public static void Info(params string[] args)
  {
    Log(Color.Cyan, [.. args, "\n"]);
  }
  
  /// <summary>
  /// Shortcut for info messages in cyan.
  /// </summary>
  public static void WriteInfo(params string[] args)
  {
    Log(Color.Cyan, [..args]);
  }

  public static void Warning(params string[] args)
  {
    Log(Color.Yellow, ["Warning: ", ..args]);
  }

  /// <summary>
  /// Shortcut for success messages in green.
  /// </summary>
  public static void Success(params string[] args)
  {
    Log(Color.Green, args);
  }
}

