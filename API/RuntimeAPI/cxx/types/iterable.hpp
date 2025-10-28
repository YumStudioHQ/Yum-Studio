/** @file iterable.hpp
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

namespace YumStudio {
/**
 * @brief Base interface for iterable container-like types in YumStudio.
 *
 * @tparam T Element type stored by the iterable.
 *
 * This abstract template provides a minimal, virtual interface for types
 * that expose contiguous, indexable storage and support pointer-based
 * iteration. Derived types are expected to override the virtual members
 * to expose their underlying data.
 *
 * Member semantics:
 * - data() should return a pointer to the first element or nullptr if empty.
 * - size() should return the number of elements.
 * - operator[](index) should return a reference to the element at the given
 *   zero-based index; behavior is undefined for out-of-range indices.
 * - begin() and end() should return pointers to the first element and one
 *   past the last element, respectively, enabling range-based for loops.
 *
 * All member functions are noexcept; default implementations may return
 * nullptr (for pointers) or 0 (for size) and therefore should be overridden
 * by concrete subclasses to provide useful behavior.
 */
  template <typename T>
  class iterable : public enable<iterable<T>> {
  private:
    T empty = T();

  public:
    inline virtual T *data() const noexcept { return nullptr; }
    inline virtual ysxlen size() const noexcept { return 0; }
    inline virtual const T &operator[](ysxlen) const { return empty; }
    inline virtual T &operator[](ysxlen) { return empty; }
    inline virtual T *begin() const noexcept { return nullptr; }
    inline virtual T *end() const noexcept { return nullptr; }
    inline virtual void foreach(const std::function<void(T&)>&) const {}
    
    inline const type_info &get_type() const override {
      return this->get_type_base({}, {});
    }
  };
}