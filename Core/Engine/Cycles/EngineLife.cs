using System;

namespace YumStudio.Core.Engine.Cycles;

#region on ready

public interface ICycleAnyAttribue {}

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
public class OnEngineReadyAttribute : Attribute, ICycleAnyAttribue { }

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
public class OnEditorReadyAttribute : Attribute, ICycleAnyAttribue { }

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
public class OnYumStudioReadyAttribute : Attribute, ICycleAnyAttribue { }

#endregion

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
public class OnEngineShutdownAttribute : Attribute, ICycleAnyAttribue { }

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
public class OnEditorShutdownAttribute : Attribute, ICycleAnyAttribue { }
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct)]
public class OnYumStudioShutdownAttribute : Attribute, ICycleAnyAttribue { }