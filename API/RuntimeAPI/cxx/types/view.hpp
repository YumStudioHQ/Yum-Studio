/** @file readonlyvec.hpp
 * 
 * This file is a part of the YumStudio Meta Engine Project.
 * This file is provided "as is," without warranty of any kind.
 * You may NOT sell this file without any modification.
 * 
 * @author MONOE.
 */

#pragma once

#include <vector>
#include <memory>
#include <cstdint>

#include "yscxx.hpp"
#include "iterable.hpp"

#include "maw/maw.hpp"
#include "maw/maw.abstract.hpp"

namespace YumStudio {
  /**
   * @brief represents an std::vector<T> but in read-only.
   * It's extremely close to the span, while this one is first of all, read-only.
   * YumStudio uses it also when communicating between C and C++. 
   * Instead of creating std::shared_ptr<object> with all elements of a vector, we just copy the vector.
   */
  template <typename T>
  class view : public enable<view, iterable<T>> {
  private:
    std::vector<T> vec;

  public:
    inline T *data() const noexcept { return vec.data(); }
    inline ysxlen size() const noexcept { return vec.size(); }
    inline T &operator[](ysxlen i) const { return vec[i]; }
    inline T *begin() const noexcept { return vec.data(); }
    inline T *end() const noexcept { return vec.data() + vec.size(); }

    inline void foreach(const std::function<void(T&)> &f) const {
      for (auto &e:vec) f(e);
    }
    
    inline const type_info &get_type() const override {
      return this->get_type_base({}, {});
    }

    inline view() {}
    inline view(const std::vector<T> &v)
      : vec(v) {}
  };
};