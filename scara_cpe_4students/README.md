# scara_cpe

Enoncé sur le [wiki](https://github.com/m0rph03nix/scara_cpe_4students/wiki)

## a commenter:

    <ros2_control name="GazeboSystem" type="system">

      <hardware>
        <plugin>gazebo_ros2_control/GazeboSystem</plugin>
      </hardware>

      <joint name="shoulder_1_joint">
      
        <command_interface name="position">
        </command_interface>     

        <state_interface name="position">
        </state_interface>


      </joint>

      <joint name="shoulder_2_joint">

        <command_interface name="position">
        </command_interface>    

        <state_interface name="position">
        </state_interface>


      </joint>    

    </ros2_control>
