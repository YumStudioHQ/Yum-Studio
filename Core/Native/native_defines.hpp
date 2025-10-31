/** ************************************* YumStudio *************************************
 * This file is provided by YumStudio itself. It is a part of the YumStudio engine.
 * By using this file, you agree YumStudio's license (https://github.com/YumStudioHQ/Yum-Studio/main/LICENSE.md)
 * 
 * This file may NOT be selled or redistributed without any modification.
 * By modifying this file, you must credit YumStudio (at least, https://github.com/YumStudioHQ/Yum-Studio)
 * 
 ** ************************************* YumStudio ************************************* */

#pragma once

#include <maw/maw.hpp>
#include <maw/maw.abstract.hpp>

#include <godot_cpp/godot.hpp>

/**
 * @brief Contains all YumStudio C++ backend in this namespace.
 */
namespace YumStudio {
 
  // Include maw inside YumStudio.
  using namespace maw;
 
  /**
   * @brief Contains all YumStudio's native tools and classes.
   * Functions here are parts of the engine.
   */
  namespace Native {

  }

  /**
   * @brief Contains YumStudio's Godot interface, and also godot_cpp's definitions.
   */
  namespace Godot {
    using namespace godot;
  }
}