from conans import ConanFile, CMake, tools
import os


class LibrdkafkaTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    build_requires = "cmake_installer/3.10.0@conan/stable"

    def build(self):
        cmake = CMake(self)

        if tools.os_info.is_windows:
            # Enables overridding of default window build settings
            cmake.definitions["WITHOUT_WIN32_CONFIG"] = "ON"

        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package".
        cmake.configure(source_dir=self.source_folder, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")

        if tools.os_info.is_linux:
            ld_lib_path = os.environ.get("LD_LIBRARY_PATH", "")
            os.environ["LD_LIBRARY_PATH"] = ld_lib_path + "."

        self.run(".%sexample" % os.sep)
