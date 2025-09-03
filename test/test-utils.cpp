#include <gtest/gtest.h>

extern "C" void utils(void);

TEST(utils, case01)
{
    utils();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
