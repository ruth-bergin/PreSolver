# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/rbergin/miniconda3/envs/nlocalsat/bin/cmake

# The command to remove a file.
RM = /home/rbergin/miniconda3/envs/nlocalsat/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils

# Include any dependencies generated for this target.
include CMakeFiles/satutils.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/satutils.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/satutils.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/satutils.dir/flags.make

CMakeFiles/satutils.dir/gen_from_solution.cpp.o: CMakeFiles/satutils.dir/flags.make
CMakeFiles/satutils.dir/gen_from_solution.cpp.o: gen_from_solution.cpp
CMakeFiles/satutils.dir/gen_from_solution.cpp.o: CMakeFiles/satutils.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/satutils.dir/gen_from_solution.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/satutils.dir/gen_from_solution.cpp.o -MF CMakeFiles/satutils.dir/gen_from_solution.cpp.o.d -o CMakeFiles/satutils.dir/gen_from_solution.cpp.o -c /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/gen_from_solution.cpp

CMakeFiles/satutils.dir/gen_from_solution.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/satutils.dir/gen_from_solution.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/gen_from_solution.cpp > CMakeFiles/satutils.dir/gen_from_solution.cpp.i

CMakeFiles/satutils.dir/gen_from_solution.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/satutils.dir/gen_from_solution.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/gen_from_solution.cpp -o CMakeFiles/satutils.dir/gen_from_solution.cpp.s

CMakeFiles/satutils.dir/satutils.cpp.o: CMakeFiles/satutils.dir/flags.make
CMakeFiles/satutils.dir/satutils.cpp.o: satutils.cpp
CMakeFiles/satutils.dir/satutils.cpp.o: CMakeFiles/satutils.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/satutils.dir/satutils.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/satutils.dir/satutils.cpp.o -MF CMakeFiles/satutils.dir/satutils.cpp.o.d -o CMakeFiles/satutils.dir/satutils.cpp.o -c /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/satutils.cpp

CMakeFiles/satutils.dir/satutils.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/satutils.dir/satutils.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/satutils.cpp > CMakeFiles/satutils.dir/satutils.cpp.i

CMakeFiles/satutils.dir/satutils.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/satutils.dir/satutils.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/satutils.cpp -o CMakeFiles/satutils.dir/satutils.cpp.s

CMakeFiles/satutils.dir/split_cnf.cpp.o: CMakeFiles/satutils.dir/flags.make
CMakeFiles/satutils.dir/split_cnf.cpp.o: split_cnf.cpp
CMakeFiles/satutils.dir/split_cnf.cpp.o: CMakeFiles/satutils.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/satutils.dir/split_cnf.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/satutils.dir/split_cnf.cpp.o -MF CMakeFiles/satutils.dir/split_cnf.cpp.o.d -o CMakeFiles/satutils.dir/split_cnf.cpp.o -c /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/split_cnf.cpp

CMakeFiles/satutils.dir/split_cnf.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/satutils.dir/split_cnf.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/split_cnf.cpp > CMakeFiles/satutils.dir/split_cnf.cpp.i

CMakeFiles/satutils.dir/split_cnf.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/satutils.dir/split_cnf.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/split_cnf.cpp -o CMakeFiles/satutils.dir/split_cnf.cpp.s

CMakeFiles/satutils.dir/stat_cnf.cpp.o: CMakeFiles/satutils.dir/flags.make
CMakeFiles/satutils.dir/stat_cnf.cpp.o: stat_cnf.cpp
CMakeFiles/satutils.dir/stat_cnf.cpp.o: CMakeFiles/satutils.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/satutils.dir/stat_cnf.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/satutils.dir/stat_cnf.cpp.o -MF CMakeFiles/satutils.dir/stat_cnf.cpp.o.d -o CMakeFiles/satutils.dir/stat_cnf.cpp.o -c /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/stat_cnf.cpp

CMakeFiles/satutils.dir/stat_cnf.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/satutils.dir/stat_cnf.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/stat_cnf.cpp > CMakeFiles/satutils.dir/stat_cnf.cpp.i

CMakeFiles/satutils.dir/stat_cnf.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/satutils.dir/stat_cnf.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/stat_cnf.cpp -o CMakeFiles/satutils.dir/stat_cnf.cpp.s

# Object files for target satutils
satutils_OBJECTS = \
"CMakeFiles/satutils.dir/gen_from_solution.cpp.o" \
"CMakeFiles/satutils.dir/satutils.cpp.o" \
"CMakeFiles/satutils.dir/split_cnf.cpp.o" \
"CMakeFiles/satutils.dir/stat_cnf.cpp.o"

# External object files for target satutils
satutils_EXTERNAL_OBJECTS =

satutils.so: CMakeFiles/satutils.dir/gen_from_solution.cpp.o
satutils.so: CMakeFiles/satutils.dir/satutils.cpp.o
satutils.so: CMakeFiles/satutils.dir/split_cnf.cpp.o
satutils.so: CMakeFiles/satutils.dir/stat_cnf.cpp.o
satutils.so: CMakeFiles/satutils.dir/build.make
satutils.so: /home/rbergin/miniconda3/envs/nlocalsat/lib/libboost_python37.so.1.71.0
satutils.so: /home/rbergin/miniconda3/envs/nlocalsat/lib/libboost_numpy37.so.1.71.0
satutils.so: /home/rbergin/miniconda3/envs/nlocalsat/lib/libboost_python37.so.1.71.0
satutils.so: CMakeFiles/satutils.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX shared module satutils.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/satutils.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/satutils.dir/build: satutils.so
.PHONY : CMakeFiles/satutils.dir/build

CMakeFiles/satutils.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/satutils.dir/cmake_clean.cmake
.PHONY : CMakeFiles/satutils.dir/clean

CMakeFiles/satutils.dir/depend:
	cd /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils /home/rbergin/PreSolver/PreSolver/NLocalSAT-master/satutils/CMakeFiles/satutils.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/satutils.dir/depend
