/// YumStudio API
/// 
/// API provided by YumStudio.
/// This is free and open-source — but please credit us!
/// (YumStudio: https://github.com/YumStudioHQ)
/// 
/// This code is provided "as is". You're responsible for
/// anything that happens when using it.
/// 
/// Thanks for using our format!
/// 
/// Author: Wys (https://github.com/wys-prog)

#pragma once

#include <memory>
#include <vector>

#define MAW_USES_LANGUAGE_MACROS
#include "Maw/maw.hpp"

#include "flow.hpp"

namespace YumStudio {
#ifndef YUM_STUDIO_CXX_ALREADY_USED_MAW
#define YUM_STUDIO_CXX_ALREADY_USED_MAW
  using namespace maw;
#endif // YUM_STUDIO_CXX_ALREADY_USED_MAW

  template <typename T>
  class HotSpot : public object {
  private:
    std::vector<std::shared_ptr<invocable>> flows;

  public:
    inline HotSpot() {}
    
    inline std::shared_ptr<object> activator() const override {
      return std::make_shared<HotSpot<T>>();
    }

    fun(HotSpot, fire, (const T &arg), {
      for (const auto &callable : flows) (*callable).call(arg);

      leave;
    })

    // TODO: Subscribe
    // TODO: Dict
    // TODO: Flow.Name

    MAW_DefEmptyTypeInfoCode(Flow, &object().get_type())
  };
}

#undef MAW_USES_LANGUAGE_MACROS