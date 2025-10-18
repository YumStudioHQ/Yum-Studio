using System.Linq;
using System.Reflection;

namespace YumStudio.Utility
{
  public static class YSObjectUtilities
  {
    public static YSObject Reflect<T>(T obj, string scope)
    {
      YSObject yso = new();
      yso[scope] = [];

      var type = typeof(T);
      var binding = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;

      var fields = type.GetFields(binding)
                       .Where(f => f.FieldType == typeof(string));

      foreach (var field in fields)
      {
        string name = field.Name;
        string value = field.GetValue(obj) as string ?? "";
        yso[scope][name] = value;
      }

      var props = type.GetProperties(binding)
                      .Where(p => p.PropertyType == typeof(string) && p.CanRead);

      foreach (var prop in props)
      {
        string name = prop.Name;
        string value = prop.GetValue(obj) as string ?? "";
        yso[scope][name] = value;
      }

      return yso;
    }
  }
}
