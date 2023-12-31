export type User = {
  id: number;
  username: string;
  name: string;
  email: string;
  roll_number: string;
};

export type Conversation = {
  id: string;
  title: string;
  owner_id: number;
  created_at: string;
};

export type Message = {
  id: string;
  role: string;
  content: string;
  conversation_id: string;
  created_at: string;
};
