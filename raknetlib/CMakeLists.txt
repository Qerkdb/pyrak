cmake_minimum_required(VERSION 3.10)

project(RakNetProject)

set(CMAKE_CXX_STANDARD 11)

if(WIN32)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /DWIN32_LEAN_AND_MEAN")
endif()

file(GLOB SOURCES "src/*.cpp")

include_directories(${CMAKE_SOURCE_DIR}/include)

add_library(RakNetLibrary SHARED ${SOURCES})

if(WIN32)
    target_link_libraries(RakNetLibrary ws2_32)  # Пример зависимости для Windows
endif()
