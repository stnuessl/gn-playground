#include <gtest/gtest.h>

extern "C" void drivers(void);

TEST(init, case01)
{
    drivers();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
