#include <csignal>
#include <iostream>
#include <string>
#include <string_view>

#include "include/downstream/dstream/dstream.hpp"

namespace {

template<typename Algo>
void process_single_input(uint64_t S, uint64_t T) {
    if (Algo::has_ingest_capacity(S, T)) {
        auto result = Algo::assign_storage_site(S, T);
        std::cout << (result ? std::to_string(*result) : "None") << '\n';
    } else {
        std::cout << '\n';
    }
}

bool process_algorithm(const std::string_view target_function) {
    using namespace downstream::dstream;

    uint64_t T, S;
    while (std::cin >> S >> T) {
        if (target_function == "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site") {
            process_single_input<hybrid_0_steady_1_stretched_2_algo>(S, T);
        }
        else if (target_function == "dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site") {
            process_single_input<hybrid_0_steady_1_tilted_2_algo>(S, T);
        }
        else if (target_function == "dstream.steady_algo.assign_storage_site") {
            process_single_input<steady_algo>(S, T);
        }
        else if (target_function == "dstream.stretched_algo.assign_storage_site") {
            process_single_input<stretched_algo>(S, T);

        }
        else if (target_function == "dstream.tilted_algo.assign_storage_site") {
            process_single_input<tilted_algo>(S, T);
        }
        else {
            std::cerr << "Error: Unknown algorithm function: " << target_function << '\n';
            return false;
        }
    }
    return true;
}

}  // namespace

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN); // Ignore broken pipe signals
    std::ios_base::sync_with_stdio(false); // Disable synchronization with C stdio for performance

    std::string_view target_function(argv[1]);
    if (!process_algorithm(target_function)) {
        return 1;
    }

    return 0;
}
