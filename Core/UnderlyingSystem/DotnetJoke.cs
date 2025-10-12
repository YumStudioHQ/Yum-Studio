using System.Collections.Generic;

namespace YumStudio.Core.UnderlyingSystem;

/// <summary>
/// Why C# and dotnet CLI are Jokes fr fr ?
/// </summary>
public static class DotnetJoke
{
  private static readonly Dictionary<int, string> Map = new()
  {
    { 0, "SUCCESS: Success -- Operation was successful." },
    { 1, "SUCCESS: Success_HostAlreadyInitialized -- Another host context already initialized." },
    { 2, "SUCCESS: Success_DifferentRuntimeProperties -- Initialized but properties differ." },
    { -2147450751, "FAILLURE: InvalidArgFailure -- One or more arguments are invalid." },
    { -2147450750, "FAILLURE: CoreHostLibLoadFailure -- Failed to load a hosting component." },
    { -2147450749, "FAILLURE: CoreHostLibMissingFailure -- A hosting component is missing." },
    { -2147450748, "FAILLURE: CoreHostEntryPointFailure -- Missing required entry point." },
    { -2147450747, "FAILLURE: CoreHostCurHostFindFailure -- Could not determine .NET installation path." },
    { -2147450745, "FAILLURE: CoreClrResolveFailure -- The coreclr library could not be found." },
    { -2147450744, "FAILLURE: CoreClrBindFailure -- Failed to load or bind to coreclr." },
    { -2147450743, "FAILLURE: CoreClrInitFailure -- Failed to initialize CoreCLR." },
    { -2147450742, "FAILLURE: CoreClrExeFailure -- coreclr_execute_assembly failed." },
    { -2147450741, "FAILLURE: ResolverInitFailure -- hostpolicy dependency resolver failed." },
    { -2147450740, "FAILLURE: ResolverResolveFailure -- Dependency resolution failed." },
    { -2147450738, "FAILLURE: LibHostInitFailure -- hostpolicy library initialization failed." },
    { -2147450735, "FAILLURE: LibHostSdkFindFailure -- Could not find requested SDK." },
    { -2147450734, "FAILLURE: LibHostInvalidArgs -- Invalid arguments to hostpolicy." },
    { -2147450733, "FAILLURE: InvalidConfigFile -- Invalid or missing runtimeconfig.json." },
    { -2147450732, "FAILLURE: AppArgNotRunnable -- CLI args don't contain an app to run." },
    { -2147450731, "FAILLURE: AppHostExeNotBoundFailure -- apphost missing imprint or broken bundle." },
    { -2147450730, "FAILLURE: FrameworkMissingFailure -- Missing or incompatible framework version." },
    { -2147450729, "FAILLURE: HostApiFailed -- Host API failed (get_native_search_directories etc)." },
    { -2147450728, "FAILLURE: HostApiBufferTooSmall -- Provided buffer was too small." },
    { -2147450726, "FAILLURE: AppPathFindFailure -- App path in apphost doesn't exist." },
    { -2147450725, "FAILLURE: SdkResolveFailure -- Failed to resolve requested SDK." },
    { -2147450724, "FAILLURE: FrameworkCompatFailure -- Framework references not compatible." },
    { -2147450723, "FAILLURE: FrameworkCompatRetry -- Framework resolution retry (bug?)" },
    { -2147450721, "FAILLURE: BundleExtractionFailure -- Corrupted or invalid single-file bundle." },
    { -2147450720, "FAILLURE: BundleExtractionIOError -- IO error extracting single-file bundle." },
    { -2147450719, "FAILLURE: LibHostDuplicateProperty -- Duplicate runtime property in config." },
    { -2147450718, "FAILLURE: HostApiUnsupportedVersion -- Hosting API version too old." },
    { -2147450717, "FAILLURE: HostInvalidState -- Invalid host state for operation." },
    { -2147450716, "FAILLURE: HostPropertyNotFound -- Requested property not found." },
    { -2147450715, "FAILLURE: HostIncompatibleConfig -- Host configuration incompatible." },
    { -2147450714, "FAILLURE: HostApiUnsupportedScenario -- Unsupported hosting API scenario." },
    { -2147450713, "FAILLURE: HostFeatureDisabled -- Requested hosting feature is disabled." }
  };

  /// <summary>
  /// Returns a human-readable description of a dotnet CLI exit code.
  /// </summary>
  public static string Describe(int code)
  {
    if (Map.TryGetValue(code, out var desc))
      return desc;
    return $"Unknown exit code: {code}";
  }

  public static bool IsSuccess(int code) => code == 0 || code == 1 || code == 2;
}