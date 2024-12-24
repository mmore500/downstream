#include <iostream>
#include <csignal>
#include "include/downstream/dstream/steady_algo/_steady_assign_storage_site.hpp"
#include "include/downstream/dstream/steady_algo/_steady_has_ingest_capacity.hpp"

using namespace downstream::dstream::steady_algo;

int main() {
    signal(SIGPIPE, SIG_IGN);
    std::ios_base::sync_with_stdio(false);
    uint64_t T, S;

    while (std::cin >> S >> T) {
        if (steady_has_ingest_capacity(S, T)) {
            auto result = steady_assign_storage_site(S, T);
            if (result) {
                std::cout << *result << '\n';
            } else {
                std::cout << "None\n";
            }
        } else {
            std::cout << "\n";
        }
    }
    return 0;
}