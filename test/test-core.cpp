#include <gtest/gtest.h>

extern "C" void core(void);

TEST(core, case01)
{
    core();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
