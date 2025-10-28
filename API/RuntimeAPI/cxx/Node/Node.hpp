/** @file Node.hpp
 * 
 * This file is a part of the YumStudio Meta Engine Project.
 * This file is provided "as is," without warranty of any kind.
 * You may NOT sell this file without any modification.
 * 
 * @author MONOE.
 */

#pragma once

#include <string>
#include <cstdint>

#include "maw/maw.hpp"
#include "maw/maw.abstract.hpp"

#include "yscxx.hpp"
#include "interface/ysnative.h"

namespace YumStudio {

  class node_not_found : public exception {
  public:
    inline node_not_found() : exception("node not found") {}
    inline node_not_found(const std::vector<std::string> &args) : exception("node not found", args) {}

    inline const type_info &get_type() const override {
      static type_info info {
        m_type_name<node_not_found>(),
        [](auto) { return std::make_shared<node_not_found>(); },
        {}, {},
        &exception().get_type()
      };
      return info;
    }
  };

  /**
   * @brief Represents a Godot/YumStudio Managed Node. Maw.Reflection is enabled on it.
   * 
   * This class uses internally UIDs based on an unsigned integer of 64 bits.
   * Even if there's 64 unsigned bits, you are limited to 18 446 744 073 709 551 614 Nodes (which is clearly enough)
   */
  class Node : public enable<Node> {
  private:
    uint64_t uid;
    const ysnative *native = ys_get_native();

  public:
    /**
     * @brief creates a new node.
     */
    inline Node() {
      uid = ys_get_native()->create();
    }

    /** 
     * @brief Builds a Node from the given uid.
     */
    inline Node(uint64_t _uid) : uid(_uid) {}

    inline Node get_node(const std::string &name) {
      auto nuid = native->get_node(name.c_str());
      if (nuid == INVALID_NODE) throw node_not_found({"cannot find node " + name});
    }

    ~Node() {
      ys_get_native()->queuefree(uid);
    }
  };
}