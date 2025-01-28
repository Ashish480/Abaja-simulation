#include "rclcpp/rclcpp.hpp"
#include "ackermann_msgs/msg/ackermann_drive.hpp"
#include <termios.h>
#include <unistd.h>
#include <iostream>
#include <string>

using std::placeholders::_1;

class AckermannControl : public rclcpp::Node
{
public:
    AckermannControl()
        : Node("ackermann_control"), speed_(0.0), steering_angle_(0.0)
    {
        publisher_ = this->create_publisher<ackermann_msgs::msg::AckermannDrive>("/cmd_ackermann", 10);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100), std::bind(&AckermannControl::timer_callback, this));
        print_instructions();
    }

private:
    rclcpp::Publisher<ackermann_msgs::msg::AckermannDrive>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    double speed_;
    double steering_angle_;

    void print_instructions()
    {
        std::cout << R"(
Ackermann Control Node
---------------------------
Moving around:
          ^
          w 
   < a    s    d >
---------------------------
w : increase speed
s : decrease speed
a : turn left
d : turn right
r : steering angle to 0
q : to stop and quit
)" << std::endl;
    }

    char getKey()
    {
        struct termios oldt, newt;
        char key;
        tcgetattr(STDIN_FILENO, &oldt);
        newt = oldt;
        newt.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        key = getchar();
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
        return key;
    }

    void timer_callback()
    {
        ackermann_msgs::msg::AckermannDrive msg;
        msg.steering_angle_velocity = M_PI / 72;
        msg.acceleration = 0.5;

        char key = getKey();

        switch (key)
        {
        case 'w':
            speed_ += 1.0;
            break;
        case 's':
            speed_ -= 1.0;
            break;
        case 'a':
            steering_angle_ -= M_PI / 36;
            break;
        case 'd':
            steering_angle_ += M_PI / 36;
            break;
        case 'r':
            steering_angle_ = 0.0;
            break;
        case 'q':
            speed_ = 0.0;
            steering_angle_ = 0.0;
            publish_message(msg);
            std::cout << "Exiting... Speed: " << speed_ << " Steering Angle: " << steering_angle_ << std::endl;
            rclcpp::shutdown();
            return;
        default:
            break;
        }

        msg.speed = speed_;
        msg.steering_angle = steering_angle_;

        publish_message(msg);
        std::cout << "Speed: " << speed_ << " | Steering Angle: " << steering_angle_ << std::endl;
    }

    void publish_message(ackermann_msgs::msg::AckermannDrive &msg)
    {
        publisher_->publish(msg);
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<AckermannControl>());
    rclcpp::shutdown();
    return 0;
}

