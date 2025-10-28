/** @file span.hpp
 * 
 * This file is a part of the YumStudio Meta Engine Project.
 * This file is provided "as is," without warranty of any kind.
 * You may NOT sell this file without any modification.
 * 
 * @author MONOE.
 */

#pragma once

#include <cstdint>

#include "yscxx.hpp"
#include "iterable.hpp"

#include "maw/maw.hpp"
#include "maw/maw.abstract.hpp"

namespace YumStudio {

  /**
   * @brief Non-owning contiguous view over a sequence of elements of type T.
   *
   * @tparam T Element type stored in the span.
   *
   * This class provides a lightweight, non-owning view into a contiguous
   * sequence (pointer + size). It offers access to the raw data pointer and
   * size, random access with bounds-checked indexing, iterator-style begin/end
   * access, and a convenience foreach that applies a callable to each element.
   *
   * Important notes:
   * - The span does not own the underlying elements. The caller must ensure
   *   the lifetime of the referenced storage outlives the span.
   * - operator[] performs a bounds check and throws std::out_of_range for
   *   invalid indexes.
   *
   * Member behavior summary:
   * - data() noexcept: returns pointer to the first element.
   * - size() noexcept: returns the number of elements (ysxlen).
   * - operator[](ysxlen at): returns reference to element at position at
   *   (throws std::out_of_range on invalid access).
   * - begin()/end() noexcept: return pointers suitable for range-based for
   *   loops and standard algorithms.
   * - foreach(const std::function<void(T&)> &f): applies f to each element
   *   in order.
   * - get_type(): returns runtime type information via get_type_base.
   *
   * Complexity:
   * - data(), size(), begin(), end(): O(1)
   * - operator[]: O(1)
   * - foreach: O(n) where n is size()
   */
  template <typename T>
  class span : public enable<span, iterable<T>> {
  private:
    T       *b;
    uint64_t s;

  public:
    inline T *data() const noexcept override { return b; }
    inline ysxlen size() const noexcept override { return s; }

    inline T &operator[](ysxlen at) const override {
      if (at > s) throw std::out_of_range("YumStudio::span: " + std::to_string(at) + " > " + std::to_string(s));

      return b[at];
    }

    inline T *begin() const noexcept override { return b; }
    inline T *end() const noexcept override { return b + s; }

    inline void foreach(const std::function<void(T&)> &f) const override {
      for (ysxlen i = 0; i < s; i++) f(s[i]);
    }

    inline const type_info &get_type() const override {
      return this->get_type_base({}, {});
    }
  };
}