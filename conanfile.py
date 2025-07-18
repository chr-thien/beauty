from conan import ConanFile, conan_version
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, rmdir
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version

import os

required_conan_version = ">=1.53.0"

class BeautyConan(ConanFile):
    name            = "beauty"
    description     = "HTTP Server above Boost.Beast"
    version         = "1.0.6"
    url             = "https://github.com/dfleury2/beauty"
    license         = "MIT"
    settings        = "os", "compiler", "build_type", "arch"
    package_type    = "library"
    options         = {
        "fPIC": [True, False],
        "shared": [True, False],
        "openssl": [True, False]
    }
    default_options = {
        "fPIC": True,
        "shared": False,
        "openssl": True
    }
    options_description = {
        "fPIC": "Enable Position Independent Code",
        "shared": "Build shared library",
        "openssl": "Enable OpenSSL support"
    }

    @property
    def _build_tests(self):
        return not self.conf.get("tools.build:skip_test", default=False, check_type=bool)

    @property
    def _build_examples(self):
        return not self.conf.get("user.beauty:skip_examples", default=False, check_type=bool)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def export_sources(self):
        copy(self, "*.hpp", dst=os.path.join(self.export_sources_folder, "include"), src=os.path.join(self.recipe_folder, "include"))
        copy(self, "*", dst=os.path.join(self.export_sources_folder, "src"), src=os.path.join(self.recipe_folder, "src"))
        copy(self, "*", dst=os.path.join(self.export_sources_folder, "tests"), src=os.path.join(self.recipe_folder, "tests"))
        copy(self, "*", dst=os.path.join(self.export_sources_folder, "examples"), src=os.path.join(self.recipe_folder, "examples"))
        copy(self, "CMakeLists.txt", dst=self.export_sources_folder, src=self.recipe_folder)
        #copy(self, "LICENSE", dst=self.export_folder, src=self.recipe_folder)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("boost/1.85.0", transitive_headers=True)
        if self.options.openssl:
            # dependency of asio in boost, exposed in boost/asio/ssl/detail/openssl_types.hpp
            self.requires("openssl/[>=1.1 <4]", transitive_headers=True, transitive_libs=True)

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, "17")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BEAUTY_ENABLE_OPENSSL"] = self.options.openssl
        tc.variables["BEAUTY_BUILD_EXAMPLES"] = self._build_examples
        tc.variables["BUILD_TESTING"] = self._build_tests
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if self._build_tests:
            cmake.test()

    def package(self):
        copy(self, "LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        cmake = CMake(self)
        cmake.install()
        copy(self, "*", dst=os.path.join(self.package_folder, "examples"),
                src=os.path.join(self.build_folder, "examples"),
                excludes=["*.cpp", "*.hpp", "*.pem", "*.txt", "*.cmake", "CMakeFiles", "bazel"])
        copy(self, "*.t", dst=os.path.join(self.package_folder, "tests"), src=os.path.join(self.build_folder, "t"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def layout(self):
        if conan_version < Version("2"):
            # package_info
            self.cpp.package.includedirs = ["include"]
            self.cpp.package.libs = ["beauty"]

            # layout info
            self.cpp.build.includedirs = ["src"]
            self.cpp.build.libdirs = ["lib"]
            self.cpp.build.libs = ["beauty"]

            self.cpp.source.includedirs = ["include"]

            # build folder detection for editable mode
            conan_folders_build = os.getenv("CONAN_FOLDERS_BUILD", "build")
            if "CONAN_FOLDERS_BUILD" not in os.environ:
                build_type = str(self.settings.build_type).lower()
                if os.path.isdir(os.path.join(self.recipe_folder, f"cmake-build-{build_type}")):
                    conan_folders_build = f"cmake-build-{build_type}"

            self.folders.build = conan_folders_build
            print(f"-- Conan folders build {self.folders.build}")
            self.folders.generators = self.folders.build

        else:
            self.cpp_info.libs = ["beauty"]
            self.cpp_info.set_property("cmake_file_name", "Beauty")
            self.cpp_info.set_property("cmake_target_name", "beauty::beauty")

            if self.settings.os in ["Linux", "FreeBSD"]:
                self.cpp_info.system_libs = ["pthread"]
            elif self.settings.os == "Windows":
                self.cpp_info.system_libs = ["crypt32"]
            if self.options.openssl:
                self.cpp_info.defines = ["BEAUTY_ENABLE_OPENSSL"]
