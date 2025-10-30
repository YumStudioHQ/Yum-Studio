/** ************************************* YumStudio *************************************
 * This file is provided by YumStudio itself. It is a part of the YumStudio engine.
 * By using this file, you agree YumStudio's license (https://github.com/YumStudioHQ/Yum-Studio/main/LICENSE.md)
 * 
 * This file may NOT be selled or redistributed without any modification.
 * By modifying this file, you must credit YumStudio (at least, https://github.com/YumStudioHQ/Yum-Studio)
 * 
 ** ************************************* YumStudio ************************************* */

#pragma once

#include <string>

#include <maw/maw.hpp>
#include <maw/maw.abstract.hpp>
#include <godot_cpp/classes/node.hpp>

#include "native_defines.hpp"

namespace YumStudio::Native {
  class SystemNode : public enable<SystemNode>, public Godot::Node {
  private:
  protected:
  public:
  };
}