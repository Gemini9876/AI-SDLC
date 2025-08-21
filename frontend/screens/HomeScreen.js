import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  ActivityIndicator,
  RefreshControl,
  Alert,
  Dimensions, // For responsiveness
  ScrollView // For accessibility and overall layout
} from 'react-native';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { getArticles, getArticleById } from '../utils/api';
import { getData } from '../utils/storage';
import ArticleCard from '../components/ArticleCard';
import { Colors } from '../styles/colors';

const HomeScreen = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const navigation = useNavigation();

  const fetchArticles = useCallback(async () => {
    setLoading(true);
    try {
      const token = await getData('userToken');
      const userJson = await getData('userInfo');
      if (userJson) {
        setUserInfo(JSON.parse(userJson));
      }
      const fetchedArticles = await getArticles(token);
      setArticles(fetchedArticles);
    } catch (error) {
      console.error('Failed to fetch articles:', error.response ? error.response.data : error.message);
      Alert.alert('Error', 'Failed to load articles. Please try again.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      fetchArticles();
    }, [fetchArticles])
  );

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchArticles();
  }, [fetchArticles]);

  const handleArticlePress = async (articleId, articleUrl, articleType) => {
    // Simulate direct navigation to a paid article URL for free users
    if (articleType === 'Paid' && userInfo?.subscription_level === 'Free') {
      // This scenario is handled by the backend /articles/{id} endpoint
      // Frontend initiates the request, backend denies access
      try {
        const token = await getData('userToken');
        await getArticleById(articleId, token); // This will throw 403
      } catch (error) {
        if (error.response && error.response.status === 403) {
          Alert.alert(
            'Access Denied',
            error.response.data.detail || 'Please upgrade your subscription to view this content.',
            [
              { text: 'Cancel', style: 'cancel' },
              { text: 'Upgrade Now', onPress: () => navigation.navigate('SubscriptionUpgrade') },
            ]
          );
        } else {
          Alert.alert('Error', 'Could not load article content.');
        }
        return; // Prevent further navigation attempt
      }
    }
    // For allowed articles, navigate to a detailed view (simulated)
    Alert.alert('Article View', `Navigating to: ${articleUrl}\nContent would be displayed here.`);
  };

  const renderItem = ({ item }) => (
    <ArticleCard 
      article={item} 
      onPress={() => handleArticlePress(item.id, item.url, item.article_type)}
      // Accessibility: ArticleCard handles its own internal accessibility
    />
  );

  // Responsive styling based on screen width
  const { width } = Dimensions.get('window');
  const isLargeScreen = width > 768; // Example breakpoint

  return (
    <View style={styles.container}>
      {loading ? (
        <ActivityIndicator size="large" color={Colors.primary} accessibilityLabel="Loading articles" />
      ) : (
        <FlatList
          data={articles}
          renderItem={renderItem}
          keyExtractor={(item) => item.id}
          contentContainerStyle={[styles.listContent, isLargeScreen && styles.listContentLarge]}
          refreshControl={
            <RefreshControl 
              refreshing={refreshing} 
              onRefresh={onRefresh} 
              colors={[Colors.primary]} 
              accessibilityLabel="Pull to refresh articles"
            />
          }
          ListEmptyComponent={(
            <Text style={styles.emptyText}>No articles available.</Text>
          )}
          // Accessibility: Focusable elements within the list (ArticleCard) should be handled by the card itself.
          // FlatList itself manages scrollability for screen readers.
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    paddingHorizontal: 10,
    paddingTop: 10, // Adjust for top navigation
  },
  listContent: {
    paddingBottom: 20, // Ensure space at the bottom
    // Responsive: On smaller screens, articles will naturally stack
  },
  listContentLarge: {
    // Example for larger screens: maybe two columns?
    // flexWrap: 'wrap',
    // flexDirection: 'row',
    // justifyContent: 'space-around',
  },
  emptyText: {
    textAlign: 'center',
    marginTop: 50,
    fontSize: 16,
    color: Colors.secondaryText,
    // WCAG: Ensure good contrast
  },
});

export default HomeScreen;
