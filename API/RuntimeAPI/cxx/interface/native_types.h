/** @file native_types.h
 * 
 * @brief Provides native types in order to communicate with the C# YumStudio API.
 * 
 * This file is a part of the YumStudio Meta Engine Project.
 * This file is provided "as is," without warranty of any kind.
 * You may NOT sell this file without any modification.
 * 
 * @author MONOE.
 */

#ifndef YSGUARD_NATIVE_TYPES
#define YSGUARD_NATIVE_TYPES

#include <stdint.h>

#include "ysctypes.h"

#define INVALID_NODE ((uint64_t)-1)

/** 
 * @brief Creates a new node
 * @return a UID of the created Node. INVALID_NODE if creation fails.
 */
typedef uint64_t (*ysnative_create)();

/**
 * @brief Queues the node to be freed.
 */
typedef void (*ysnative_queuefree)(uint64_t);

/**
 * @brief Gives children of the given Node.
 */
typedef void (*ysnative_get_children)(uint64_t, uint64_t*, uint64_t);

/**
 * @brief Returns the parent's UID related to the given Node.
 * @return parent's UID.
 */
typedef uint64_t (*ysnative_get_parent)(uint64_t);

/**
 * @brief Returns parents' UID related to the given Node.
 */
typedef void (*ysnative_get_parents)(uint64_t, uint64_t*, uint64_t);

/**
 * @brief Returns an UID representing the asked Node.
 * @param NodeName
 * @return a UID to the related Node. INVALID_NODE if get_node fails.
 */
typedef uint64_t (*ysnative_get_node)(const char*);

/**
 * @brief Adds the second Node to the first one.
 * @note Prefer using ysnative_add_children when you have to add several children to a node.
 * @param Parent
 * @param NewChild
 */
typedef void (*ysnative_add_child)(uint64_t, uint64_t);

/**
 * @brief Adds the given array of Node to the first node.
 * @param Parent
 * @param Nodes
 * @param Count
 */
typedef void (*ysnative_add_children)(uint64_t, uint64_t*, uint64_t);

/**
 * @brief Connects the given signal to the given node. Once the signal fired, the callback will be called.
 * @param Node
 * @param MethodName
 * @param Callback
 */
typedef void (*ysnative_connect)(uint64_t, const char*, ysgd_callback);

/**
 * @brief represents a YumStudio C(++) module Native Backend.
 */
typedef struct {
  ysnative_add_child    add_child;
  ysnative_add_children add_children;
  ysnative_connect      connect;
  ysnative_get_node     get_node;
  ysnative_get_parent   get_parent;
  ysnative_get_parents  get_parents;
  ysnative_create       create;
  ysnative_queuefree    queuefree; 
} ysnative;

#endif // YSGUARD_NATIVE_TYPES