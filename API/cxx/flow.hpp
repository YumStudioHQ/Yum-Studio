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
#include "maw/maw.hpp"
#define _MAW_BACKEND
#include "maw/_maw.hpp"

namespace YumStudio {
#ifndef YUM_STUDIO_CXX_ALREADY_USED_MAW
#define YUM_STUDIO_CXX_ALREADY_USED_MAW
  using namespace maw;
#endif // YUM_STUDIO_CXX_ALREADY_USED_MAW

  template <typename T>
  class Flow : public object {
  private:
    std::shared_ptr<invocable> base;
    std::string name_;

  public:
    inline Flow() {}
    inline Flow(std::shared_ptr<invocable> &inv, const std::string &n = "unnamed") : base(inv), name_(n) {}
    
    inline std::shared_ptr<object> activator() const override {
      return std::make_shared<Flow<T>>();
    }

    inline fun(Flow, call, (const T &arg), {
      ret (*base).invoke({arg});
    })

    inline fun(Flow, name, (), {
      ret literal<std::string>(name_);
    })

    MAW_DefEmptyTypeInfoCode(Flow, &object().get_type())
  };
}

#undef MAW_USES_LANGUAGE_MACROS