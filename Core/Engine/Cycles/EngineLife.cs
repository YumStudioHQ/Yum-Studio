using System;

namespace YumStudio.Core.Engine.Cycles;

#region on ready

[AttributeUsage(AttributeTargets.Class)]
public class OnEngineReadyAttribute : Attribute { }

[AttributeUsage(AttributeTargets.Class)]
public class OnEditorReadyAttribute : Attribute { }

[AttributeUsage(AttributeTargets.Class)]
public class OnYumStudioReadyAttribute : Attribute { }

#endregion

[AttributeUsage(AttributeTargets.Class)]
public class OnEngineShutdownAttribute : Attribute { }