/** @file array.hpp
 * 
 * This file is a part of the YumStudio Meta Engine Project.
 * This file is provided "as is," without warranty of any kind.
 * You may NOT sell this file without any modification.
 * 
 * @author MONOE.
 */

#pragma once

#include <cstdint>
#include <functional>

#include "yscxx.hpp"

#include "maw/maw.hpp"
#include "maw/maw.abstract.hpp"

#include "iterable.hpp"

namespace YumStudio {
  template <typename T, size_t S>
  class array : public iterable<T> {
  private:
    T *me;
    bool onstack = false;

  public:
    inline const type_info &get_type() const override {
      static type_info info {
        m_type_name<array<T, S>>(),
        [](auto) { return std::make_shared<array<T, S>>(); },
        {}, {},
        &iterable<T>().get_type()
      };

      return info;
    }

    inline T *data() const noexcept override { return me; }
    inline ysxlen size() const noexcept override { return S; }
    
    inline T &operator[](ysxlen i) override { 
      if (i >= S) throw std::out_of_range(std::string(m_type_name(*this)));
      return me[i];
    }
        
    inline const T &operator[](ysxlen i) const override { 
      if (i >= S) throw std::out_of_range(std::string(m_type_name(*this)));
      return me[i];
    }

    inline T *begin() const noexcept override { return me; }
    inline T *end() const noexcept override { return me + S; }

    inline void foreach(const std::function<void(T&)> &f) const override {
      for (ysxlen i = 0; i < S; i++) f(me[i]);
    }

    inline void fill(const T &with) {
      for (ysxlen i = 0; i < S; i++) me[i] = with;
    }

    inline array(T *a) 
      : me(a), onstack(false) {}
    
    inline array() : me(nullptr), onstack(true) {
      me = new T[S];
    }

    inline ~array() {
      if (onstack) {
        delete[] me;
      }
    }
  };
}