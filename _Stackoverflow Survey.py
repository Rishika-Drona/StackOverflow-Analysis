#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd

df = pd.read_csv('C:/Users/rishi/Desktop/Python projects/online survey Analysis/survey_results_public.csv')
df.head()


# In[13]:


df.shape


# In[14]:


#The value_counts() function looks at a single column of data at a time and counts how many instances of each unique entry that column contains.
# We need to do is tell Python the specific Series (a.k.a. column) we want to look at, and then tell it to execute .value_counts(). We can specify a specific column by writing the name of the dataframe, followed by the name of the column inside brackets
# 'BetterLife' is a string of characters rather than a number or a variable name, we need to put it inside apostrophes or quotation marks to keep Python from getting confused
df['BetterLife'].value_counts()


# In[15]:


# Nrmalizing the counts by representing them as a percentage of the total number of rows in the pandas series we’ve specified.

df['BetterLife'].value_counts(normalize = True)


# In[16]:


# Another Yes/No question: “Do you believe that you need to be a manager to make more money?”

df['MgrMoney'].value_counts(normalize = True)


# In[17]:


# Plotting of multiple choice answers
get_ipython().run_line_magic('matplotlib', 'inline')


# In[19]:


# Adding a little snippet to the end of our code: .plot(kind='bar'). This tells Python to take whatever we’ve just given it and plot the results in a bar graph. (We could replace 'bar' with 'pie' to get a pie chart instead, if we want)

df['SocialMedia'].value_counts().plot(kind="bar")


# In[21]:


# Changing the color and the figure size

df['SocialMedia'].value_counts().plot(kind="bar", figsize=(15,7), color="pink")


# In[22]:


# Analysing the Subsets byfiltering for only the responses in that Series that meet a certain criteria by using a conditional operator.

said_no = df[df['BetterLife']=='No']
said_no.head(3)


# In[23]:


# To confirm that this worked, we can check the size of this dataset with .shape, and compare the number of rows in said_no to the number of people who answered ‘No’ to that question, using our old friend .value_counts()

said_no.shape


# In[24]:


df['BetterLife'].value_counts()


# In[25]:


# We can further confirm the filter has worked by running a quick value_counts() on this new dataframe.

said_no['BetterLife'].value_counts()


# In[26]:


# taking a backtrack and a deeper look at the code then,

said_no =df[ df['BetterLife']=='No']

#said_no = is telling Python to create a new variable called said_no, and make it equal to whatever’s on the right side of the equals sign.
#df is telling Python to make said_no equivalent to the df DataFrame (our original data set)
#[df['BetterLife'] == 'No'] is telling Python to only include rows from df in which the answer in the 'BetterLife' column is equal to 'No'.


# In[27]:


# Now that we have this dataframe containing only the ‘No’ answerers, let’s make an equivalent one for the ‘Yes’ folks and then run some comparisons.

said_yes = df[df['BetterLife'] == 'Yes']


# In[28]:


# We’ll use a couple of new tricks in this code: .mean() and .median() functions, which will automatically calculate the mean and median, respectively, of a column of numerical data. We’re also going to enclose our calculations within a print() command so that all four numbers will be printed at once.

print(said_no['Age'].mean(),
      said_yes['Age'].mean(),
      said_no['Age'].median(),
      said_yes['Age'].median()
     )

# As we can see here, the pessimists tended to be slightly older, but not by a significant margin. It might be interesting to look at how specific age groups answered this question and whether that differed. 


# In[32]:


# finding out using the same Boolean trick we’ve been using, but instead of using == to check our conditional, we’ll use >= and <= since we want to filter for respondents whose 'Age' were 50 and up or 25 and down.

over50 = df[df['Age'] >= 50]
under25 = df[df['Age'] <= 25]


print(over50['BetterLife'].value_counts(normalize=True))
print(under25['BetterLife'].value_counts(normalize=True))


# It looks like the oldest devs really are quite pessimistic, with slightly more than half of them saying that children born today won’t have a better life than their parents. Young devs, on the other hand, seem to be more optimistic than average.


# In[33]:


# Using the len() function, which will count the number of items in a list or rows in a DataFrame.

print(len(over50))
print(len(under25))


# In[34]:


# Filtering more specific subsets by change from using a single Boolean is that when we’re stringing together more than one, we need to enclose each Boolean in parentheses, so the basic format looks like this: df[(Boolean 1) & (Boolean 2)]

filtered_1 = df[(df['BetterLife'] == 'Yes') & (df['Country'] == 'India')]


print(filtered_1['BetterLife'].value_counts())
print(filtered_1['Country'].value_counts())

# our new DataFrame, filtered_1, contains only people in India who gave the optimistic answer about the future.


# In[35]:


filtered = df[(df['BetterLife'] == 'Yes') & (df['Age'] >= 50) & (df['Country'] == 'India') &~ (df['Hobbyist'] == "Yes") &~ (df['OpenSourcer'] == "Never")]
filtered


# In[36]:


# Analysing multi-answer survey questions. first task is to take a look at the relevant column to see how answers were recorded in this particular survey.

df["LanguageWorkedWith"].head()


# In[37]:


# using the argument normalize=True to view the results as percentages rather than seeing the raw counts.

python_bool = df["LanguageWorkedWith"].str.contains('Python')
python_bool.value_counts(normalize=True)


# In[38]:


# running that code on the 'LanguageWorkedWith' column and store the results as a new pandas series called lang_lists.

lang_lists = df["LanguageWorkedWith"].str.split(';', expand=True)
lang_lists.head()


# In[42]:


# As we can see, our string splitting worked. Each row in our series is now a row in the new data frame, and each language has been split from the others into unique columns.

#But we wanted to figure out how many times each language was mentioned, and we’re not done yet. value_counts() won’t help us here — we can only use that on a pandas Series, not a DataFrame.

#To be able to see the number of times each language was mentioned in total, we have to do a bit more work. There are a number of ways we could approach this problem, but here’s one:

#Use df.stack() to stack this DataFrame, slicing each column and then stacking them on top of each other so that every data point in the DataFrame appears in a single pandas Series.

#Use value_counts() on this new “stacked” series to get the total number of times each language is mentioned.

#This is a bit complicated, so let’s try this with a simpler example first so we can observe what’s happening visually. We’ll start with a DataFame that’s very similar to lang_lists, just a lot shorter so that it’s easier to follow.

lang_lists


# In[44]:


lang_lists.stack()


# In[45]:


lang_lists.stack().value_counts()


# In[47]:


# That’s the information we were looking for! Now, let’s put a final touch on our analysis project by charting this information visually, using the same approach to plotting we used earlier.

lang_lists.stack().value_counts().plot(kind='bar', figsize=(15,7), color="#61d199")


# In[ ]:




