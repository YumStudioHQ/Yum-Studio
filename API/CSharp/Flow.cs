using System;

namespace YumStudio.API;

/// <summary>
/// Represents a single action, with the parameter T.
/// </summary>
/// <typeparam name="T">Argument type</typeparam>
public partial class Flow<T>
{
  private Action<T> self;

  /// <summary>
  /// Labels the Flow<T>. That name can be (or not) unique.
  /// </summary>
  public string Name { get; private set; } = $"Flow<{typeof(T).FullName}>-{Guid.NewGuid()}";

  public Flow() { }
  public Flow(Action<T> action) { self = action; }
  public Flow(string name, Action<T> action) { self = action; Name = name; }

  /// <summary>
  /// Calls the internal Action<T> with arg. Can throw Exceptions.
  /// </summary>
  /// <param name="arg">Argument</param>
  public void Call(T arg) => self(arg);

  /// <summary>
  /// Indicates Flow's validity.
  /// </summary>
  public bool IsValid => self != null;

  /// <summary>
  /// Tries to call the Action. Won't get invoked if the given function is null.
  /// </summary>
  /// <param name="arg">Argument</param>
  public void SafeCall(T arg) => self?.Invoke(arg);
}

public partial class Flow
{
  private Action self;
  public string Name { get; private set; } = $"Flow-{Guid.NewGuid()}";

  public Flow() { }
  public Flow(Action action) { self = action; }
  public Flow(string name, Action action) { self = action; Name = name; }

  /// <summary>
  /// Calls the internal Action<T> with arg. Can throw Exceptions.
  /// </summary>
  public void Call() => self();

  /// <summary>
  /// Indicates Flow's validity.
  /// </summary>
  public bool IsValid => self != null;

  /// <summary>
  /// Tries to call the Action. Won't get invoked if the given function is null.
  /// </summary>
  public void SafeCall() => self?.Invoke();
}