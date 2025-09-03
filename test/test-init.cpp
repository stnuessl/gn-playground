#include <gtest/gtest.h>

extern "C" void init(void);

TEST(init, case01)
{
    init();
}

int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
