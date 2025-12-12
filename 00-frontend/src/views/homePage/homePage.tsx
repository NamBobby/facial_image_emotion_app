import React from "react";
import { View, Text, TouchableOpacity} from "react-native";
import HomeStyle from "../../styles/homeStyle";
import { useNavigation } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";
import { RootStackParamList } from "../../navigations/AppNavigator";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, "Home">;

const Home = () => {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  const navigateToShooting = () => {
    navigation.navigate("Shooting");
  };

  return (
    <View style={HomeStyle.container}>
      <View style={HomeStyle.topinfo}>
      <View style={HomeStyle.frame}>
            <Text style={HomeStyle.textframe}>Emotion Detect</Text>
      </View>
        <View style={HomeStyle.buttonmenu}>
          <View style={HomeStyle.option}>
            <TouchableOpacity style={HomeStyle.rectangle} onPress={navigateToShooting}>
              <View style={HomeStyle.option}>
                <FontAwesomeIcon icon={faMagnifyingGlass} size={40} color="#FFFFFF" />
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </View>
  );
};

export default Home;