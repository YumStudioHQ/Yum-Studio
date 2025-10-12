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

#define MAW_USES_LANGUAGE_MACROS
#include "Maw/maw.hpp"

namespace YumStudio {
#ifndef YUM_STUDIO_CXX_ALREADY_USED_MAW
#define YUM_STUDIO_CXX_ALREADY_USED_MAW
  using namespace maw;
#endif // YUM_STUDIO_CXX_ALREADY_USED_MAW

  template <typename T>
  class Flow : public object {
  private:
    std::shared_ptr<invocable> base;

  public:
    inline Flow() {}
    inline Flow(std::shared_ptr<invocable> &inv) : base(inv) {}
    
    inline std::shared_ptr<object> activator() const override {
      return std::make_shared<Flow<T>>();
    }


    fun(Flow, call, (const T &arg), {
      ret (*base).invoke({arg});
    })

    MAW_DefEmptyTypeInfoCode(Flow, &object().get_type())
  };
}

#undef MAW_USES_LANGUAGE_MACROS